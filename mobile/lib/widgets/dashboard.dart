import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:hairstyle/widgets/chatbot.dart';
import 'package:hairstyle/widgets/recommendation.dart';

class Dashboard extends StatelessWidget {
  const Dashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Hairstyle Recommendation',
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(
          title: Text('De RAIN Barbershop',
                style: TextStyle(fontSize: 30.0, color: Colors.amber[600])),
          centerTitle: true,
          backgroundColor: Colors.black),
        body: Container(
          width: 10000,
          color: Colors.black87,
          padding: EdgeInsets.all(20),
          child: Column(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                SizedBox(
                  width: 400.0,
                  height: 70.0,
                  child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          primary: Colors.amber[600],
                          shape: StadiumBorder(),
                        ),
                    onPressed: () async {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (context) => Recomendation(),
                        ),
                      );
                    },
                    child: Text('START',
                    style : TextStyle(fontSize: 36)),
                  ),
                ),

                SizedBox(
                  width: 400.0,
                  height: 70.0,
                  child: FloatingActionButton.large(
                    onPressed: () async {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (context) => Chatbot(),
                        ),
                      );
                    },
                    backgroundColor: Colors.white,
                    child: Icon(Icons.chat_bubble, color: Colors.amber[600]),
                  )
                )
              ]),
        ),
      ),
    );
  }
}
