import 'package:equatable/equatable.dart';
import 'transaction.dart';

class Category extends Equatable {
  final int? id;
  final String name;
  final String? description;
  final String? icon;
  final String? color;
  final TransactionType type;
  final bool isActive;
  final DateTime createdAt;
  final DateTime updatedAt;

  const Category({
    this.id,
    required this.name,
    this.description,
    this.icon,
    this.color,
    required this.type,
    this.isActive = true,
    required this.createdAt,
    required this.updatedAt,
  });

  @override
  List<Object?> get props => [
        id,
        name,
        description,
        icon,
        color,
        type,
        isActive,
        createdAt,
        updatedAt,
      ];

  Category copyWith({
    int? id,
    String? name,
    String? description,
    String? icon,
    String? color,
    TransactionType? type,
    bool? isActive,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return Category(
      id: id ?? this.id,
      name: name ?? this.name,
      description: description ?? this.description,
      icon: icon ?? this.icon,
      color: color ?? this.color,
      type: type ?? this.type,
      isActive: isActive ?? this.isActive,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }
}
