import '../entities/wallet.dart';

abstract class WalletRepository {
  Future<List<Wallet>> getWallets();
  Future<Wallet> getWallet(int id);
  Future<Wallet> createWallet(Wallet wallet);
  Future<Wallet> updateWallet(Wallet wallet);
  Future<void> deleteWallet(int id);
  Future<double> getWalletBalance(int id);
  Future<void> recalculateWalletBalance(int id);
}
