import 'package:flutter/material.dart';
import 'login.dart';
void main(){
  runApp(StayPay());
}
class StayPay extends StatelessWidget {
  const StayPay({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(),
      initialRoute: '/',
      routes: {
        '/':(context) => Login() ,
      },
    );
  }
}