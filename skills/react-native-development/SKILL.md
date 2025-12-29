---
name: react-native-development
description: Use when building cross-platform mobile apps with React Native, Redux, and native modules.
---

# React Native Development

Build cross-platform mobile applications using React Native with modern hooks, robust state management via Redux Toolkit, and seamless native module integration.

## Quick Start

```javascript
// Functional Component with React Hooks
import React, { useEffect, useState } from 'react';
import { View, FlatList, ActivityIndicator } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { fetchUsers } from './userSlice';

export const UserListScreen = () => {
  const dispatch = useDispatch();
  const { data: users, loading, error } = useSelector(state => state.users);

  useEffect(() => {
    dispatch(fetchUsers());
  }, [dispatch]);

  if (loading) return <ActivityIndicator size="large" />;
  if (error) return <Text>Error: {error}</Text>;

  return (
    <FlatList
      data={users}
      keyExtractor={item => item.id.toString()}
      renderItem={({ item }) => <UserCard user={item} />}
    />
  );
};

// Redux Toolkit Slice
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

export const fetchUsers = createAsyncThunk(
  'users/fetchUsers',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/users');
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const userSlice = createSlice({
  name: 'users',
  initialState: { data: [], loading: false, error: null },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUsers.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchUsers.fulfilled, (state, action) => {
        state.data = action.payload;
        state.loading = false;
      })
      .addCase(fetchUsers.rejected, (state, action) => {
        state.error = action.payload;
        state.loading = false;
      });
  },
});

export default userSlice.reducer;

// Native Module Integration
import { NativeModules } from 'react-native';
const { CameraModule } = NativeModules;

export const capturePhoto = async () => {
  try {
    const photo = await CameraModule.takePicture();
    return photo;
  } catch (error) {
    console.error('Camera error:', error);
  }
};
```

## Key Concepts

- **React Hooks**: Build functional components with useState, useEffect, useContext for state and lifecycle management
- **Redux Toolkit**: Simplified Redux with reducers, async thunks, and middleware for predictable state management
- **Native Modules**: Bridge JavaScript with native code (Swift/Kotlin) for platform-specific functionality

## Common Patterns

- **Navigation**: Implement React Navigation with stack, tab, and drawer navigators for app structure
- **Async Operations**: Use Redux Toolkit's createAsyncThunk for handling API calls and side effects
- **Custom Hooks**: Create reusable hooks for common patterns like data fetching and authentication
- **Native Module Binding**: Create TypeScript definitions for native modules to maintain type safety

## Best Practices

✅ Use Redux Toolkit instead of vanilla Redux for less boilerplate
✅ Leverage React Hooks for state management in components
✅ Implement Hermes JavaScript engine for better app performance
✅ Type check with TypeScript and PropTypes for reliability
✅ Keep business logic separated from UI components

## Common Pitfalls

❌ Using class components instead of functional components with hooks
❌ Not memoizing components causing unnecessary re-renders
❌ Improper error handling in async Redux thunks
❌ Creating circular dependencies in Redux selectors
❌ Blocking main thread with heavy computations instead of using workers

## Resources

- [React Native Documentation](https://reactnative.dev/docs/getting-started)
- [Redux Toolkit Documentation](https://redux-toolkit.js.org/)
- [React Navigation Guide](https://reactnavigation.org/docs/getting-started)
- [Native Modules Integration](https://reactnative.dev/docs/native-modules-intro)
- [Hermes Engine](https://hermesengine.dev/)
- [React Hooks Documentation](https://react.dev/reference/react/hooks)
