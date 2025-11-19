---
name: android-kotlin-development
description: Use when building modern Android applications with Kotlin, Jetpack Compose, and MVVM architecture.
---

# Android Kotlin Development

Master modern Android development using Kotlin with Jetpack Compose for declarative UI, reactive architecture patterns, and efficient data management.

## Quick Start

```kotlin
// Jetpack Compose UI with MVVM
@Composable
fun UserScreen(viewModel: UserViewModel = hiltViewModel()) {
    val users by viewModel.users.collectAsState()

    LazyColumn {
        items(users) { user ->
            UserCard(user)
        }
    }
}

// MVVM ViewModel with Coroutines
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {
    val users: StateFlow<List<User>> = repository.getUsers()
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    fun deleteUser(id: Int) {
        viewModelScope.launch {
            repository.deleteUser(id)
        }
    }
}

// Room Database
@Entity
data class User(
    @PrimaryKey val id: Int,
    val name: String,
    val email: String
)

@Dao
interface UserDao {
    @Query("SELECT * FROM user")
    fun getAllUsers(): Flow<List<User>>

    @Insert
    suspend fun insertUser(user: User)
}
```

## Key Concepts

- **Jetpack Compose**: Declarative UI framework that replaces XML layouts with composable functions
- **MVVM Architecture**: Separation of concerns with ViewModel handling business logic and state management
- **Coroutines**: Kotlin's lightweight threading solution for asynchronous operations and non-blocking I/O

## Common Patterns

- **State Management**: Use StateFlow and LiveData for reactive data binding
- **Dependency Injection**: Implement Hilt for constructor injection and lifecycle-aware dependencies
- **Room Persistence**: Abstract SQLite database access with DAO pattern for type-safe queries
- **Material Design 3**: Apply theming and components from Material 3 for modern, consistent UI

## Best Practices

✅ Use StateFlow over LiveData for better performance in Compose
✅ Keep ViewModels focused on business logic, not UI rendering
✅ Leverage Hilt for dependency injection to improve testability
✅ Use Flow for streams and StateFlow for state values
✅ Implement proper error handling with try-catch in coroutines

## Common Pitfalls

❌ Blocking main thread with synchronous database calls instead of using suspend functions
❌ Creating new ViewModel instances instead of using hiltViewModel() in Compose
❌ Forgetting to cancel coroutines, leading to memory leaks
❌ Not implementing proper database migrations for Room schema changes

## Resources

- [Jetpack Compose Documentation](https://developer.android.com/jetpack/compose)
- [Android Architecture Patterns](https://developer.android.com/architecture)
- [Kotlin Coroutines Guide](https://kotlinlang.org/docs/coroutines-overview.html)
- [Room Database Tutorial](https://developer.android.com/training/data-storage/room)
- [Hilt Dependency Injection](https://developer.android.com/training/dependency-injection/hilt-android)
- [Material Design 3 for Android](https://m3.material.io/)
