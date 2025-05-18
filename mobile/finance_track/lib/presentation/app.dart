import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../data/datasources/local/database_helper.dart';
import '../data/datasources/remote/api_client.dart';
import '../data/repositories/auth_repository_impl.dart';
import '../domain/repositories/auth_repository.dart';
import 'bloc/auth/auth_bloc.dart';
import 'bloc/auth/auth_event.dart';
import 'bloc/auth/auth_state.dart';
import 'screens/home_screen.dart';
import 'screens/login_screen.dart';
import 'screens/splash_screen.dart';

class App extends StatelessWidget {
  final String baseUrl;

  const App({super.key, required this.baseUrl});

  @override
  Widget build(BuildContext context) {
    return MultiRepositoryProvider(
      providers: [
        RepositoryProvider<ApiClient>(
          create: (context) => ApiClient(baseUrl: baseUrl),
        ),
        RepositoryProvider<DatabaseHelper>(
          create: (context) => DatabaseHelper.instance,
        ),
        RepositoryProvider<AuthRepository>(
          create: (context) => AuthRepositoryImpl(
            apiClient: context.read<ApiClient>(),
          ),
        ),
      ],
      child: BlocProvider(
        create: (context) => AuthBloc(
          authRepository: context.read<AuthRepository>(),
        )..add(CheckAuthStatusEvent()),
        child: MaterialApp(
          title: 'Finance Track',
          theme: ThemeData(
            primarySwatch: Colors.blue,
            visualDensity: VisualDensity.adaptivePlatformDensity,
          ),
          home: BlocBuilder<AuthBloc, AuthState>(
            builder: (context, state) {
              if (state is AuthInitial) {
                return const SplashScreen();
              } else if (state is AuthAuthenticated) {
                return const HomeScreen();
              } else if (state is AuthUnauthenticated) {
                return const LoginScreen();
              } else {
                return const SplashScreen();
              }
            },
          ),
        ),
      ),
    );
  }
}
