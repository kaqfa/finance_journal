import '../entities/transaction.dart';

abstract class TransactionRepository {
  Future<List<Transaction>> getTransactions({
    DateTime? startDate,
    DateTime? endDate,
    int? walletId,
    int? categoryId,
    TransactionType? type,
  });
  Future<Transaction> getTransaction(int id);
  Future<Transaction> createTransaction(Transaction transaction);
  Future<Transaction> updateTransaction(Transaction transaction);
  Future<void> deleteTransaction(int id);
  Future<List<Transaction>> getRecentTransactions({int limit = 10});
  Future<Map<String, double>> getTransactionSummary({
    DateTime? startDate,
    DateTime? endDate,
    int? walletId,
  });
}
