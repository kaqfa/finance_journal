import 'package:equatable/equatable.dart';

class Wallet extends Equatable {
  final int? id;
  final String name;
  final String type;
  final double balance;
  final String? description;
  final bool isActive;
  final DateTime createdAt;
  final DateTime updatedAt;

  const Wallet({
    this.id,
    required this.name,
    required this.type,
    required this.balance,
    this.description,
    this.isActive = true,
    required this.createdAt,
    required this.updatedAt,
  });

  @override
  List<Object?> get props => [
        id,
        name,
        type,
        balance,
        description,
        isActive,
        createdAt,
        updatedAt,
      ];

  Wallet copyWith({
    int? id,
    String? name,
    String? type,
    double? balance,
    String? description,
    bool? isActive,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return Wallet(
      id: id ?? this.id,
      name: name ?? this.name,
      type: type ?? this.type,
      balance: balance ?? this.balance,
      description: description ?? this.description,
      isActive: isActive ?? this.isActive,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }
}
