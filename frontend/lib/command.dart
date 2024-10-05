import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class CommandPage extends StatefulWidget {
  const CommandPage({super.key});

  @override
  State<CommandPage> createState() => _CommandPageState();
}

class _CommandPageState extends State<CommandPage> {
  final TextEditingController _commandController = TextEditingController();
  final TextEditingController _responseController = TextEditingController();
  bool _isLoading = false;

  Future<void> _addCommand() async {
    if (_commandController.text.isEmpty || _responseController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content: Text("Please enter a command and response."),
      ));
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      var response = await http.post(
        Uri.parse(
            'http://your-flask-server-url/commands'), // Replace with your Flask API URL
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "name": _commandController.text,
          "response": _responseController.text,
        }),
      );

      if (response.statusCode == 201) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content: Text("Command added successfully!"),
        ));
      } else {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content: Text("Failed to add command."),
        ));
      }
    } catch (e) {
      print(e);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text("Error occurred: $e"),
      ));
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Manage Commands')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _commandController,
              decoration: const InputDecoration(labelText: 'Enter Command'),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _responseController,
              decoration:
                  const InputDecoration(labelText: 'Enter Command Response'),
            ),
            const SizedBox(height: 10),
            _isLoading
                ? const CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: _addCommand,
                    child: const Text('Add Command'),
                  ),
          ],
        ),
      ),
    );
  }
}
