---
name: graphql-api-design
description: Design efficient GraphQL APIs with schemas, resolvers, and DataLoader. Use when building query/mutation APIs with proper error handling.
---

# GraphQL API Design

Master GraphQL architecture with type-safe schemas, efficient resolvers using DataLoader, and comprehensive error handling for modern API development.

## Quick Start

```typescript
import { ApolloServer, gql } from 'apollo-server-express';
import express from 'express';

const typeDefs = gql`
  type Query {
    user(id: ID!): User
    users: [User!]!
  }

  type User {
    id: ID!
    email: String!
    name: String!
    posts: [Post!]!
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    author: User!
  }
`;

const resolvers = {
  Query: {
    user: async (_, { id }, { dataloaders }) => {
      return dataloaders.userLoader.load(id);
    },
    users: async (_, __, { prisma }) => {
      return prisma.user.findMany();
    }
  },
  User: {
    posts: async (user, _, { dataloaders }) => {
      return dataloaders.postsByUserLoader.load(user.id);
    }
  }
};

const server = new ApolloServer({ typeDefs, resolvers });
const app = express();
await server.start();
server.applyMiddleware({ app });
app.listen(4000, () => console.log('GraphQL server running on port 4000'));
```

## Key Concepts

### DataLoader for N+1 Prevention
```typescript
import DataLoader from 'dataloader';

const createDataloaders = (prisma: PrismaClient) => ({
  userLoader: new DataLoader(async (userIds: readonly string[]) => {
    const users = await prisma.user.findMany({
      where: { id: { in: userIds as string[] } }
    });

    const userMap = new Map(users.map(u => [u.id, u]));
    return userIds.map(id => userMap.get(id) || null);
  }),

  postsByUserLoader: new DataLoader(async (userIds: readonly string[]) => {
    const posts = await prisma.post.findMany({
      where: { userId: { in: userIds as string[] } }
    });

    const postsMap = new Map<string, any[]>();
    userIds.forEach(id => postsMap.set(id as string, []));
    posts.forEach(post => {
      postsMap.get(post.userId)?.push(post);
    });

    return userIds.map(id => postsMap.get(id as string) || []);
  })
});
```

### Schema Design with Mutations
```typescript
const typeDefs = gql`
  input CreateUserInput {
    email: String!
    name: String!
    password: String!
  }

  input UpdateUserInput {
    name: String
    email: String
  }

  type Mutation {
    createUser(input: CreateUserInput!): UserPayload!
    updateUser(id: ID!, input: UpdateUserInput!): UserPayload!
    deleteUser(id: ID!): DeletePayload!
  }

  type UserPayload {
    user: User
    errors: [FieldError!]
  }

  type DeletePayload {
    success: Boolean!
    message: String!
  }

  type FieldError {
    field: String!
    message: String!
  }
`;

const resolvers = {
  Mutation: {
    createUser: async (_, { input }, { prisma }) => {
      try {
        const emailExists = await prisma.user.findUnique({
          where: { email: input.email }
        });

        if (emailExists) {
          return {
            user: null,
            errors: [{ field: 'email', message: 'Email already in use' }]
          };
        }

        const user = await prisma.user.create({
          data: {
            email: input.email,
            name: input.name,
            password: await hashPassword(input.password)
          }
        });

        return { user, errors: [] };
      } catch (error) {
        return {
          user: null,
          errors: [{ field: 'general', message: 'Failed to create user' }]
        };
      }
    },

    updateUser: async (_, { id, input }, { prisma }) => {
      try {
        const user = await prisma.user.update({
          where: { id },
          data: input
        });
        return { user, errors: [] };
      } catch (error) {
        return {
          user: null,
          errors: [{ field: 'id', message: 'User not found' }]
        };
      }
    }
  }
};
```

### Subscriptions for Real-Time Updates
```typescript
const typeDefs = gql`
  type Subscription {
    userCreated: User!
    postUpdated(userId: ID!): Post!
  }
`;

const resolvers = {
  Subscription: {
    userCreated: {
      subscribe: (_, __, { pubsub }) => {
        return pubsub.asyncIterator(['USER_CREATED']);
      }
    },
    postUpdated: {
      subscribe: (_, { userId }, { pubsub }) => {
        return pubsub.asyncIterator([`POST_UPDATED_${userId}`]);
      }
    }
  },
  Mutation: {
    createUser: async (_, { input }, { prisma, pubsub }) => {
      const user = await prisma.user.create({ data: input });
      pubsub.publish('USER_CREATED', { userCreated: user });
      return { user, errors: [] };
    }
  }
};
```

## Common Patterns

### Custom Scalar Types and Validation
```typescript
import { GraphQLScalarType } from 'graphql';

const dateScalar = new GraphQLScalarType({
  name: 'DateTime',
  serialize: (value: Date) => value.toISOString(),
  parseValue: (value: string) => new Date(value),
  parseLiteral: (ast) => {
    if (ast.kind === Kind.STRING) {
      return new Date(ast.value);
    }
    return null;
  }
});

const typeDefs = gql`
  scalar DateTime

  type Post {
    id: ID!
    title: String!
    createdAt: DateTime!
    updatedAt: DateTime!
  }
`;

const resolvers = {
  DateTime: dateScalar
};
```

### Directives for Authorization
```typescript
const typeDefs = gql`
  directive @auth(role: String!) on FIELD_DEFINITION

  type Query {
    adminDashboard: String @auth(role: "ADMIN")
    userProfile: User @auth(role: "USER")
  }
`;

const authDirective = {
  resolve: async (resolve, source, args, context) => {
    if (!context.user) {
      throw new AuthenticationError('Not authenticated');
    }

    if (!hasRole(context.user, args.role)) {
      throw new AuthorizationError('Insufficient permissions');
    }

    return resolve();
  }
};
```

### Error Handling and Validation
```typescript
class GraphQLError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 400
  ) {
    super(message);
  }
}

const resolvers = {
  Mutation: {
    updatePost: async (_, { id, input }, { prisma }) => {
      if (!input.title?.trim()) {
        throw new GraphQLError(
          'Title is required',
          'VALIDATION_ERROR',
          400
        );
      }

      try {
        const post = await prisma.post.update({
          where: { id },
          data: input
        });
        return { post, errors: [] };
      } catch (error) {
        if (error instanceof prisma.PrismaClientKnownRequestError) {
          throw new GraphQLError(
            'Post not found',
            'NOT_FOUND',
            404
          );
        }
        throw error;
      }
    }
  }
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
  formatError: (error) => ({
    message: error.message,
    code: error.extensions?.code || 'INTERNAL_ERROR'
  })
});
```

## Best Practices

✅ Use DataLoader to prevent N+1 query problems
✅ Design schemas with clear separation of input types
✅ Return error payload objects instead of throwing errors for expected failures
✅ Implement field-level authorization with directives
✅ Use subscriptions judiciously for truly real-time requirements
✅ Validate input at the resolver level with proper error messages
✅ Batch database queries when possible
✅ Use fragments in client queries to optimize response payloads

## Common Pitfalls

❌ Fetching related data in resolvers without batching (N+1 queries)
❌ Throwing GraphQL errors for validation failures instead of returning payloads
❌ Exposing database errors directly to clients
❌ Creating overly complex nested queries without depth limits
❌ Missing input validation on mutations
❌ Not implementing proper authentication/authorization checks
❌ Returning sensitive data in error messages
❌ Subscriptions without proper cleanup causing memory leaks

## Resources

- [Apollo Server Documentation](https://www.apollographql.com/docs/apollo-server/)
- [GraphQL Official Specification](https://spec.graphql.org/)
- [DataLoader for Batching](https://github.com/graphql/dataloader)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [Schema Design Guide](https://www.apollographql.com/docs/apollo-server/schema/schema/)
