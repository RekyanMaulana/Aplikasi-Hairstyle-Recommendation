import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class Chatbot extends StatefulWidget {
  _ChatbotState createState() => _ChatbotState();
}

class _ChatbotState extends State<Chatbot> {
  final List<Message> _msg = <Message>[];
  final TextEditingController _txtController = TextEditingController();
  void getChatbotReply(String userReply) async {
    _txtController.clear();
    var response =
        await http.post(Uri.parse("http://192.168.79.165:5000/chatbot"),
            headers: <String, String>{
              'Content-Type': 'application/json; charset=UTF-8',
            },
            body: jsonEncode(<String, String>{
              'message': userReply,
            }));
    var data = jsonDecode(response.body);
    var botReply = data["answer"];
    Message msg = Message(
      text: botReply,
      name: "Bot",
      type: false,
    );
    setState(() {
      _msg.insert(0, msg);
    });
  }

  void handleSubmitted(text) async {
    if (kDebugMode) {
      print(text);
    }
    _txtController.clear();
    Message msg = Message(
      text: text,
      name: "YOU",
      type: true,
    );
    setState(() {
      _msg.insert(0, msg);
    });
    getChatbotReply(text);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Chatbot', style: TextStyle(color: Colors.amber[600]),),
        centerTitle: true,
        backgroundColor: Colors.black,
      ),
      backgroundColor: Colors.grey,
      body: Column(
        children: [
          Flexible(
              child: ListView.builder(
            padding: const EdgeInsets.all(8.0),
            reverse: true,
            itemBuilder: (_, int index) => _msg[index],
            itemCount: _msg.length,
          )),
          const Divider(height: 1.0),
          Container(
            decoration: BoxDecoration(color: Theme.of(context).cardColor),
            child: IconTheme(
              data: IconThemeData(color: Theme.of(context).cardColor),
              child: Container(
                margin: const EdgeInsets.symmetric(horizontal: 8.0),
                child: Row(
                  children: [
                    Flexible(
                      child: TextField(
                        controller: _txtController,
                        onSubmitted: handleSubmitted,
                        decoration: const InputDecoration.collapsed(
                            hintText: 'Type message'),
                      ),
                    ),
                    Container(
                      margin: const EdgeInsets.symmetric(horizontal: 4.0),
                      child: IconButton(
                        icon: const Icon(Icons.send),
                        onPressed: () => handleSubmitted(_txtController.text),
                        color: Colors.amber,
                      ),
                    )
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class Message extends StatelessWidget {
  final String text;
  final String name;
  final bool type;
  
  const Message({
    required this.text,
    required this.name,
    required this.type,
  });

  List<Widget> bot(context) {
    return <Widget>[
      Container(
        margin: const EdgeInsets.only(right: 16.0),
        child: const CircleAvatar(
          backgroundColor: Colors.amber,
          child: Icon(
              Icons.adb,
              size: 35,
              color: Colors.black,
            ),),
      ),
      Expanded(
          child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            margin: const EdgeInsets.only(top: 5.0),
            child: Text(text, style: const TextStyle(fontSize: 20.0)),
          )
        ],
      ))
    ];
  }

  List<Widget> me(context) {
    return <Widget>[
      Expanded(
          child: Column(
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Container(
            //color: Colors.white,
            margin: const EdgeInsets.only(top: 5.0),
            child: Text(text, style: const TextStyle(fontSize: 20.0)),
          )
        ],
      )),
      Container(
          margin: const EdgeInsets.only(left: 16.0),
          child: const CircleAvatar(
              backgroundColor: Colors.black,
              child: Icon(
              Icons.person_pin,
              size: 35,
              color: Colors.amber,
            ),)),
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Container(
        margin: const EdgeInsets.symmetric(vertical: 10.0),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: type ? me(context) : bot(context),
        ));
  }
}
