import '../entities/user.dart';

abstract class AuthRepository {
  Future<User> login(String username, String password);
  Future<User> register(String username, String email, String password);
  Future<void> logout();
  Future<User> getCurrentUser();
  Future<void> saveAuthToken(String token);
  Future<String?> getAuthToken();
  Future<void> clearAuthToken();
  Future<bool> isLoggedIn();
}
