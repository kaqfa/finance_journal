import 'package:flutter/material.dart';
import 'presentation/app.dart';

void main() {
  runApp(const App(baseUrl: 'http://localhost:8000'));
}

// class MainApp extends StatelessWidget {
//   const MainApp({super.key});

//   @override
//   Widget build(BuildContext context) {
//     return const MaterialApp(
//       home: Scaffold(
//         body: Center(
//           child: Text('Hello World!'),
//         ),
//       ),
//     );
//   }
// }
