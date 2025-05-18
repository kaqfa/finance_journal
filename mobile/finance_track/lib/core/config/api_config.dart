class ApiConfig {
  static const String baseUrl = 'http://localhost:8000/api/v1';
  static const String authEndpoint = '/auth';
  static const String financeEndpoint = '/finance';

  // Auth Endpoints
  static String get loginUrl => '$baseUrl$authEndpoint/login/';
  static String get registerUrl => '$baseUrl$authEndpoint/register/';
  static String get logoutUrl => '$baseUrl$authEndpoint/logout/';

  // Wallet Endpoints
  static String get walletsUrl => '$baseUrl$financeEndpoint/wallets/';
  static String walletDetailUrl(int id) => '$walletsUrl$id/';

  // Transaction Endpoints
  static String get transactionsUrl => '$baseUrl$financeEndpoint/transactions/';
  static String transactionDetailUrl(int id) => '$transactionsUrl$id/';

  // Category Endpoints
  static String get categoriesUrl => '$baseUrl$financeEndpoint/categories/';
  static String categoryDetailUrl(int id) => '$categoriesUrl$id/';
}
