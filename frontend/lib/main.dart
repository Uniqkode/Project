import 'package:flutter/material.dart';
import 'broadcast.dart';
import 'command.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Bot Admin',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const AdminPage(),
    );
  }
}

class AdminPage extends StatelessWidget {
  const AdminPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Bot Admin Interface'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => BroadcastPage()),
                );
              },
              child: const Text('Broadcast Message'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => CommandPage()),
                );
              },
              child: const Text('Manage Commands'),
            ),
          ],
        ),
      ),
    );
  }
}
