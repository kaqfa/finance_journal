import 'package:equatable/equatable.dart';

enum TransactionType { income, expense }

class Transaction extends Equatable {
  final int? id;
  final int walletId;
  final int categoryId;
  final TransactionType type;
  final double amount;
  final String description;
  final DateTime date;
  final DateTime createdAt;
  final DateTime updatedAt;

  const Transaction({
    this.id,
    required this.walletId,
    required this.categoryId,
    required this.type,
    required this.amount,
    required this.description,
    required this.date,
    required this.createdAt,
    required this.updatedAt,
  });

  @override
  List<Object?> get props => [
        id,
        walletId,
        categoryId,
        type,
        amount,
        description,
        date,
        createdAt,
        updatedAt,
      ];

  Transaction copyWith({
    int? id,
    int? walletId,
    int? categoryId,
    TransactionType? type,
    double? amount,
    String? description,
    DateTime? date,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return Transaction(
      id: id ?? this.id,
      walletId: walletId ?? this.walletId,
      categoryId: categoryId ?? this.categoryId,
      type: type ?? this.type,
      amount: amount ?? this.amount,
      description: description ?? this.description,
      date: date ?? this.date,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }
}
