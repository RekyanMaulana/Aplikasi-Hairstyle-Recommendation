import 'package:flutter/material.dart';
import 'dart:io';
import 'dart:convert';

class Result extends StatelessWidget {
  final List<dynamic> image;
  final dynamic face;
  const Result({Key? key, required this.image, required this.face}): super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          title: Text('Result', style: TextStyle(color: Colors.amber[600])),
          centerTitle: true,
          backgroundColor: Colors.black),
      body: SingleChildScrollView(
        child: Column(
          children: <Widget>[
            Container(
          color: Colors.black87,
          width: double.infinity,
          padding: EdgeInsets.all(5),
          child: Column(children: [
            Text("Bentuk Wajah : $face", style: TextStyle(color: Colors.white, fontSize: 20),),
            ListView.builder(
                scrollDirection: Axis.vertical,
                shrinkWrap: true,
                padding: const EdgeInsets.all(5),
                itemCount: image.length,
                itemBuilder: (BuildContext context, int index) {
                  return Container(
                    width: 155,
                    height: 155,
                    padding: EdgeInsets.all(3),
                    child: Image.network(
                        'http://192.168.79.165:5000/static/images/recommendation/' +
                            image[index]),
                  );
                })
          ]
          )
      )]),
    )
    );
  }
}
