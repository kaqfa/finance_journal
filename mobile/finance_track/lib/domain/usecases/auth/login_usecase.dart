import '../../entities/user.dart';
import '../../repositories/auth_repository.dart';

class LoginUseCase {
  final AuthRepository repository;

  LoginUseCase(this.repository);

  Future<User> execute(String username, String password) async {
    final user = await repository.login(username, password);
    return user;
  }
}
