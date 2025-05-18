import '../../domain/entities/wallet.dart';
import '../../domain/repositories/wallet_repository.dart';
import '../datasources/remote/api_client.dart';
import '../datasources/local/database_helper.dart';

class WalletRepositoryImpl implements WalletRepository {
  final ApiClient _apiClient;
  final DatabaseHelper _dbHelper;

  WalletRepositoryImpl({
    required ApiClient apiClient,
    required DatabaseHelper dbHelper,
  })  : _apiClient = apiClient,
        _dbHelper = dbHelper;

  @override
  Future<List<Wallet>> getWallets() async {
    try {
      final response = await _apiClient.get('/api/v1/finance/wallets/');
      final List<dynamic> walletsJson = response.data;
      return walletsJson.map((json) => _walletFromJson(json)).toList();
    } catch (e) {
      // Fallback to local data if network request fails
      final db = await _dbHelper.database;
      final List<Map<String, dynamic>> maps = await db.query('wallets');
      return List.generate(maps.length, (i) => _walletFromMap(maps[i]));
    }
  }

  @override
  Future<Wallet> getWallet(int id) async {
    try {
      final response = await _apiClient.get('/api/v1/finance/wallets/$id/');
      return _walletFromJson(response.data);
    } catch (e) {
      final db = await _dbHelper.database;
      final List<Map<String, dynamic>> maps = await db.query(
        'wallets',
        where: 'id = ?',
        whereArgs: [id],
      );
      if (maps.isNotEmpty) {
        return _walletFromMap(maps.first);
      }
      throw Exception('Wallet not found');
    }
  }

  @override
  Future<Wallet> createWallet(Wallet wallet) async {
    try {
      final response = await _apiClient.post(
        '/api/v1/finance/wallets/',
        data: _walletToJson(wallet),
      );
      final newWallet = _walletFromJson(response.data);

      // Save to local database
      final db = await _dbHelper.database;
      await db.insert('wallets', _walletToMap(newWallet));

      return newWallet;
    } catch (e) {
      rethrow;
    }
  }

  @override
  Future<Wallet> updateWallet(Wallet wallet) async {
    try {
      final response = await _apiClient.put(
        '/api/v1/finance/wallets/${wallet.id}/',
        data: _walletToJson(wallet),
      );
      final updatedWallet = _walletFromJson(response.data);

      // Update local database
      final db = await _dbHelper.database;
      await db.update(
        'wallets',
        _walletToMap(updatedWallet),
        where: 'id = ?',
        whereArgs: [wallet.id],
      );

      return updatedWallet;
    } catch (e) {
      rethrow;
    }
  }

  @override
  Future<void> deleteWallet(int id) async {
    try {
      await _apiClient.delete('/api/v1/finance/wallets/$id/');

      // Delete from local database
      final db = await _dbHelper.database;
      await db.delete(
        'wallets',
        where: 'id = ?',
        whereArgs: [id],
      );
    } catch (e) {
      rethrow;
    }
  }

  @override
  Future<double> getWalletBalance(int id) async {
    try {
      final wallet = await getWallet(id);
      return wallet.balance;
    } catch (e) {
      rethrow;
    }
  }

  @override
  Future<void> recalculateWalletBalance(int id) async {
    try {
      await _apiClient.post('/api/v1/finance/wallets/$id/recalculate/');
    } catch (e) {
      rethrow;
    }
  }

  // Helper methods for JSON/Map conversion
  Map<String, dynamic> _walletToJson(Wallet wallet) {
    return {
      'name': wallet.name,
      'type': wallet.type,
      'balance': wallet.balance,
      'description': wallet.description,
      'is_active': wallet.isActive ? 1 : 0,
    };
  }

  Map<String, dynamic> _walletToMap(Wallet wallet) {
    return {
      'id': wallet.id,
      'name': wallet.name,
      'type': wallet.type,
      'balance': wallet.balance,
      'description': wallet.description,
      'is_active': wallet.isActive ? 1 : 0,
      'created_at': wallet.createdAt.toIso8601String(),
      'updated_at': wallet.updatedAt.toIso8601String(),
    };
  }

  Wallet _walletFromJson(Map<String, dynamic> json) {
    return Wallet(
      id: json['id'],
      name: json['name'],
      type: json['type'],
      balance: json['balance'].toDouble(),
      description: json['description'],
      isActive: json['is_active'] == 1,
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  Wallet _walletFromMap(Map<String, dynamic> map) {
    return Wallet(
      id: map['id'],
      name: map['name'],
      type: map['type'],
      balance: map['balance'],
      description: map['description'],
      isActive: map['is_active'] == 1,
      createdAt: DateTime.parse(map['created_at']),
      updatedAt: DateTime.parse(map['updated_at']),
    );
  }
}
