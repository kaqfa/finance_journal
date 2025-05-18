import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/remote/api_client.dart';

class AuthRepositoryImpl implements AuthRepository {
  final ApiClient _apiClient;
  final FlutterSecureStorage _storage;

  AuthRepositoryImpl({
    required ApiClient apiClient,
    FlutterSecureStorage? storage,
  })  : _apiClient = apiClient,
        _storage = storage ?? const FlutterSecureStorage();

  @override
  Future<User> login(String username, String password) async {
    try {
      final response = await _apiClient.post('/api/v1/auth/login/', data: {
        'username': username,
        'password': password,
      });

      final token = response.data['token'];
      await _storage.write(key: 'auth_token', value: token);

      return User(
        id: response.data['user']['id'],
        username: response.data['user']['username'],
        email: response.data['user']['email'],
        token: token,
      );
    } catch (e) {
      rethrow;
    }
  }

  @override
  Future<User> register(String username, String email, String password) async {
    try {
      final response = await _apiClient.post('/api/v1/auth/register/', data: {
        'username': username,
        'email': email,
        'password': password,
      });

      final token = response.data['token'];
      return User(
        id: response.data['id'],
        username: response.data['username'],
        email: response.data['email'],
        token: token,
      );
    } catch (e) {
      rethrow;
    }
  }

  @override
  Future<void> logout() async {
    try {
      await _apiClient.post('/api/v1/auth/logout/');
      await clearAuthToken();
    } catch (e) {
      rethrow;
    }
  }

  @override
  Future<User> getCurrentUser() async {
    try {
      final response = await _apiClient.get('/api/v1/auth/profile/');
      final token = await getAuthToken() ?? '';
      return User(
        id: response.data['id'],
        username: response.data['username'],
        email: response.data['email'],
        token: token,
      );
    } catch (e) {
      rethrow;
    }
  }

  @override
  Future<void> saveAuthToken(String token) async {
    await _storage.write(key: 'auth_token', value: token);
  }

  @override
  Future<String?> getAuthToken() async {
    return await _storage.read(key: 'auth_token');
  }

  @override
  Future<void> clearAuthToken() async {
    await _storage.delete(key: 'auth_token');
  }

  @override
  Future<bool> isLoggedIn() async {
    final token = await getAuthToken();
    return token != null;
  }
}
