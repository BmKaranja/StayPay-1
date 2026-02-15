import 'package:flutter/material.dart';

class AppDetForm extends StatefulWidget {
  const AppDetForm({super.key});
  @override
  State<AppDetForm> createState() => _AppDetFormState();
}

class _AppDetFormState extends State<AppDetForm> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _aptnamecontroller =TextEditingController();
  // ignore: non_constant_identifier_names
  final TextEditingController _no_hsecontroller =TextEditingController();
  // ignore: non_constant_identifier_names
  final TextEditingController _c_namecontroller =TextEditingController();
  // ignore: non_constant_identifier_names
  final TextEditingController _c_nocontroller =TextEditingController();
  Function no_go(){
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Fill in the form'))
    );
  }
  void dispode
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: true,
      appBar: AppBar(
        title: Text('StayPay', style: TextStyle(fontWeight: FontWeight.w500),),
        backgroundColor: Color(0xFF090c11),
        foregroundColor: Color(0xFF00ff00),
      ),
      bottomNavigationBar: BottomNavigationBar(
        selectedItemColor: Color(0xFF00FF00),
        // ignore: use_full_hex_values_for_flutter_colors
        unselectedItemColor: Color(0xFF88888),
        onTap: no_go(),
        items: [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home',),
          BottomNavigationBarItem(icon: Icon(Icons.dashboard), label: 'Dashboard'),
          BottomNavigationBarItem(icon: Icon(Icons.account_circle_rounded), label: 'Account')
        ],
      ),
      body:SingleChildScrollView(
        padding: EdgeInsets.all(10),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                decoration: InputDecoration(labelText: 'Apartment Name'),
                controller: _aptnamecontroller,
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Total Number of Houses'),
                controller: _no_hsecontroller,
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Carataker Name'),
                controller: _c_namecontroller,
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Caretaker Phone Number'),
                controller: _c_nocontroller,
              ),
              ElevatedButton(onPressed:()=>{
                // ignore: avoid_print
                print('Apartment details: $_aptnamecontroller, $_no_hsecontroller, $_c_namecontroller, $_c_nocontroller '),
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