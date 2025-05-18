import '../../entities/transaction.dart';
import '../../repositories/transaction_repository.dart';

class GetRecentTransactionsUseCase {
  final TransactionRepository repository;

  GetRecentTransactionsUseCase(this.repository);

  Future<List<Transaction>> execute({int limit = 10}) async {
    return await repository.getRecentTransactions(limit: limit);
  }
}
