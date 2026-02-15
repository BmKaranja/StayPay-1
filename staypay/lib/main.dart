import 'package:flutter/material.dart';
import 'splash.dart';
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
      initialRoute: "/splash",
      routes: {
        '/splash':(context) => const SplashScreen(),
        '/login':(context) => const LoginScreen(),
      },
    );
  }
}