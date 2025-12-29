---
name: flutter-development
description: Use when building cross-platform mobile apps with Flutter, Dart, and native platform integration.
---

# Flutter Development

Create beautiful, performant cross-platform mobile applications using Flutter's widget composition system, reactive state management patterns, and seamless native platform integration.

## Quick Start

```dart
// Flutter Widget with Provider State Management
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class UserListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Users')),
      body: Consumer<UserProvider>(
        builder: (context, userProvider, _) {
          if (userProvider.isLoading) {
            return Center(child: CircularProgressIndicator());
          }
          return ListView.builder(
            itemCount: userProvider.users.length,
            itemBuilder: (context, index) {
              return UserCard(user: userProvider.users[index]);
            },
          );
        },
      ),
    );
  }
}

// Provider State Management
import 'package:provider/provider.dart';

class UserProvider extends ChangeNotifier {
  List<User> _users = [];
  bool _isLoading = false;

  List<User> get users => _users;
  bool get isLoading => _isLoading;

  Future<void> loadUsers() async {
    _isLoading = true;
    notifyListeners();

    try {
      _users = await UserRepository().fetchUsers();
    } catch (e) {
      print('Error loading users: $e');
    }

    _isLoading = false;
    notifyListeners();
  }

  Future<void> deleteUser(int id) async {
    _users.removeWhere((user) => user.id == id);
    notifyListeners();
    await UserRepository().deleteUser(id);
  }
}

// Async/Await Pattern in Dart
class UserRepository {
  Future<List<User>> fetchUsers() async {
    try {
      final response = await http.get(Uri.parse('/api/users'));
      if (response.statusCode == 200) {
        return (jsonDecode(response.body) as List)
            .map((user) => User.fromJson(user))
            .toList();
      }
    } on SocketException {
      throw Exception('Network error');
    }
    throw Exception('Failed to load users');
  }
}

// Platform Channels for Native Integration
import 'package:flutter/services.dart';

class NativeInterop {
  static const platform = MethodChannel('com.example.app/native');

  static Future<String> takePhoto() async {
    try {
      final String result = await platform.invokeMethod('takePicture');
      return result;
    } on PlatformException catch (e) {
      return "Failed to take photo: '${e.message}'";
    }
  }
}
```

## Key Concepts

- **Widget Composition**: Build UIs by combining reusable widgets in a tree structure for declarative, reactive interfaces
- **State Management**: Use Provider or Riverpod for efficient, scalable state management with ChangeNotifier patterns
- **Dart Async**: Leverage Futures, async/await, and Streams for non-blocking asynchronous operations

## Common Patterns

- **Platform Channels**: Communicate between Flutter and native code (Swift/Kotlin) for device-specific features
- **Material & Cupertino Designs**: Implement Material Design 3 for Android and Cupertino styles for iOS
- **Custom Widgets**: Create reusable stateful and stateless widgets to encapsulate UI and logic
- **Dependency Injection**: Use service locators like GetIt for managing dependencies across the app

## Best Practices

✅ Use Provider or Riverpod for predictable, testable state management
✅ Prefer Stateless widgets and rebuild on state changes over Stateful widgets
✅ Implement proper error handling with try-catch in Future chains
✅ Use const constructors to reduce widget rebuild overhead
✅ Leverage Hot Reload during development for faster iteration

## Common Pitfalls

❌ Overusing Stateful widgets when Provider/Riverpod would be cleaner
❌ Not disposing resources (controllers, listeners) causing memory leaks
❌ Blocking the main thread with synchronous operations instead of using async/await
❌ Ignoring platform-specific UI patterns (Material vs Cupertino)
❌ Creating inefficient build methods with unnecessary widget rebuilds

## Resources

- [Flutter Documentation](https://flutter.dev/docs)
- [Dart Language Guide](https://dart.dev/guides)
- [Provider State Management](https://pub.dev/packages/provider)
- [Riverpod Guide](https://riverpod.dev/)
- [Platform Channels Tutorial](https://flutter.dev/docs/development/platform-integration/platform-channels)
- [Material Design 3 Components](https://m3.material.io/)
- [Cupertino Widgets Reference](https://flutter.dev/docs/development/ui/widgets/cupertino)
