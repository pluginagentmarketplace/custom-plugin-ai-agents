---
name: ios-swift-development
description: Use when building iOS applications with SwiftUI, Combine, async/await, and MVVM patterns.
---

# iOS Swift Development

Build robust iOS applications using SwiftUI for declarative interfaces, Combine for reactive programming, and modern async/await concurrency patterns.

## Quick Start

```swift
// SwiftUI View with MVVM
struct UserListView: View {
    @StateObject private var viewModel = UserViewModel()

    var body: some View {
        NavigationStack {
            List(viewModel.users) { user in
                NavigationLink(destination: UserDetailView(user: user)) {
                    UserRow(user: user)
                }
            }
            .navigationTitle("Users")
            .task {
                await viewModel.loadUsers()
            }
        }
    }
}

// MVVM ViewModel with Combine and async/await
@MainActor
class UserViewModel: ObservableObject {
    @Published var users: [User] = []
    @Published var isLoading = false

    private let repository: UserRepository

    init(repository: UserRepository = .shared) {
        self.repository = repository
    }

    func loadUsers() async {
        isLoading = true
        do {
            users = try await repository.fetchUsers()
        } catch {
            print("Error loading users: \(error)")
        }
        isLoading = false
    }
}

// Core Data Model
@Model
final class User {
    var id: UUID
    var name: String
    var email: String
    var createdAt: Date

    init(id: UUID = UUID(), name: String, email: String, createdAt: Date = .now) {
        self.id = id
        self.name = name
        self.email = email
        self.createdAt = createdAt
    }
}
```

## Key Concepts

- **SwiftUI**: Declarative framework using property wrappers (@State, @Published, @StateObject) for reactive UI updates
- **Combine**: Reactive framework for handling asynchronous events and data streams with Publishers and Subscribers
- **async/await**: Modern concurrency syntax that makes asynchronous code readable and eliminates callback hell

## Common Patterns

- **Property Wrappers**: Use @State, @ObservedObject, @EnvironmentObject for managing view state
- **MVVM Architecture**: Separate concerns with ViewModel handling data operations and view logic
- **Combine Operators**: Chain operators like map, filter, sink for data transformation pipelines
- **SwiftData/Core Data**: Persist application data with type-safe models and efficient queries

## Best Practices

✅ Use @MainActor on ViewModels to ensure UI updates occur on main thread
✅ Leverage property wrappers to keep views lightweight and reactive
✅ Combine async/await with Task for cleaner concurrency patterns
✅ Use SwiftData for new apps, Core Data for legacy support
✅ Implement proper error handling with do-try-catch blocks

## Common Pitfalls

❌ Creating ObservableObject without @MainActor leading to thread safety issues
❌ Keeping @Published publishers in View instead of ViewModel
❌ Not canceling Combine subscriptions causing memory leaks
❌ Using @EnvironmentObject without proper injection in preview
❌ Blocking the main thread with synchronous operations

## Resources

- [SwiftUI Documentation](https://developer.apple.com/documentation/swiftui)
- [Combine Framework Guide](https://developer.apple.com/documentation/combine)
- [Swift Concurrency with async/await](https://developer.apple.com/wwdc21/10132)
- [Core Data Tutorial](https://developer.apple.com/documentation/coredata)
- [SwiftData Documentation](https://developer.apple.com/documentation/swiftdata)
- [MVVM Pattern for iOS](https://www.raywenderlich.com/36-mvvm-tutorial-for-ios)
