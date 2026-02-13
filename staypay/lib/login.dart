import 'package:flutter/material.dart';

class Login extends StatefulWidget {
  const Login({super.key});

  @override
  State<Login> createState() => _LoginState();
}

class _LoginState extends State<Login> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  // Tenant controllers
  final TextEditingController _tenantHouseNumberController = TextEditingController();
  final TextEditingController _tenantPasswordController = TextEditingController();

  // Landlord controllers
  final TextEditingController _landlordEmailController = TextEditingController();
  final TextEditingController _landlordPasswordController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF090C11),
      appBar: AppBar(
        backgroundColor: const Color(0xFF090C11),
        bottom: TabBar(
          controller: _tabController,
          indicatorColor: const Color(0xFF00FF00),
          tabs: const [
            Tab(text: "Tenant Login"),
            Tab(text: "Landlord Login"),
          ],
        ),
        title: const Text("StayPay Rent Management"),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildTenantLogin(),
          _buildLandlordLogin(),
        ],
      ),
    );
  }

  Widget _buildTenantLogin() {
    return Padding(
      padding: const EdgeInsets.all(20.0),
      child: Column(
        children: [
          _buildTextField("House Number", _tenantHouseNumberController),
          const SizedBox(height: 20),
          _buildTextField("Password", _tenantPasswordController, obscure: true),
          const SizedBox(height: 30),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF00FF00),
              ),
              onPressed: () {
              },
              child: const Text("Login", style: TextStyle(color: Colors.white)),
            ),
          ),
          const SizedBox(height: 15),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
              onPressed: () {
                // ignore: avoid_print
                print("Tenant SignUp: ${_tenantHouseNumberController.text}");
              },
              child: const Text("Sign Up", style: TextStyle(color: Colors.white)),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLandlordLogin() {
    return Padding(
      padding: const EdgeInsets.all(20.0),
      child: Column(
        children: [
          _buildTextField("Email", _landlordEmailController),
          const SizedBox(height: 20),
          _buildTextField("Password", _landlordPasswordController, obscure: true),
          const SizedBox(height: 30),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
            onPressed: () {
            },
            child: const Text("Login", style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }

  Widget _buildTextField(String label, TextEditingController controller, {bool obscure = false}) {
    return TextField(
      controller: controller,
      obscureText: obscure,
      decoration: InputDecoration(
        labelText: label,
        border: const OutlineInputBorder(),
      ),
    );
  }
}
/*Widget type mismatch  
You declared Login as a StatelessWidget but then tried to use createState(). Only StatefulWidget should have createState.

dart
class Login extends StatefulWidget { // ✅ should be StatefulWidget
  const Login({super.key});

  @override
  State<Login> createState() => _LoginState();
}
Typos in method names

_buildTenatLogin → should be _buildTenantLogin.

padding → should be Padding (capital P).

Style: → should be style: (lowercase).

ElevatedButton.StyleFrom → should be ElevatedButton.styleFrom.

Controller names mismatch  
You declared _tenantHousenumbercontroller but used tenantHouseController. They must match.

Return type of helper methods  
_buildTenantLogin() should return a Widget, not widget.*/