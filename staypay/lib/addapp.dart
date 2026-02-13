import 'package:flutter/material.dart';

class AppDetForm extends StatefulWidget {
  const AppDetForm({super.key});
  @override
  State<AppDetForm> createState() => _AppDetFormState();
}

class _AppDetFormState extends State<AppDetForm> {
  final _formKey = GlobalKey<FormState>();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: true,
      appBar: AppBar(
        title: Text('Apartment details'),
        backgroundColor: Color(0xFF00FF00),
        foregroundColor: Colors.black,
      ),
      body:SingleChildScrollView(
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                decoration: InputDecoration(labelText: 'Apartment Name'),
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Total Number of Houses'),
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Carataker Name'),
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Caretaker Phone Number'),
              ),
              ElevatedButton(onPressed:()=>{
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('✅Saved successfully'),backgroundColor: Color(0xFF00FF00),)
                )
              } , child: Text('Save'))
            ],  
                  
          )
        ),
      ),
    );
  }
}