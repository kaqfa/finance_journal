import '../../entities/wallet.dart';
import '../../repositories/wallet_repository.dart';

class GetWalletsUseCase {
  final WalletRepository repository;

  GetWalletsUseCase(this.repository);

  Future<List<Wallet>> execute() async {
    return await repository.getWallets();
  }
}
