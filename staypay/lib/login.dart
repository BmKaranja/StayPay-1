import 'package:flutter/material.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  // Tenant controllers
  final TextEditingController tenantHouseController = TextEditingController();
  final TextEditingController tenantPasswordController = TextEditingController();

  // Landlord controllers
  final TextEditingController landlordEmailController = TextEditingController();
  final TextEditingController landlordPasswordController = TextEditingController();

  // SignUp controllers (inside landlord tab)
  final TextEditingController fullNameController = TextEditingController();
  final TextEditingController signupEmailController = TextEditingController();
  final TextEditingController phoneController = TextEditingController();
  final TextEditingController signupPasswordController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this); // Tenant & Landlord tabs
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFF090c11),
      appBar: AppBar(
        backgroundColor: Color(0xFF090c11),
        bottom: TabBar(
          controller: _tabController,
          indicatorColor: Color(0xFF00ff00),
          tabs: const [
            Tab(text: "Tenant"),
            Tab(text: "Landlord"),
          ],
        ),
        title: const Text("StayPay RENT MANAGEMENT"),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildTenantLogin(),
          _buildLandlordAuth(),
        ],
      ),
    );
  }

  Widget _buildTenantLogin() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(20.0),
      child: Column(
        children: [
          Image.asset("assets/logo.png", height: 80),
          const SizedBox(height: 20),
          _buildTextField("House Number", tenantHouseController),
          const SizedBox(height: 20),
          _buildTextField("Password", tenantPasswordController, obscure: true),
          TextButton(
            onPressed: () => Navigator.pushNamed(context, "/tenantReset"),
            child: const Text("Forgot Password?", style: TextStyle(color: Color(0xFF00ff00))),
          ),
          const SizedBox(height: 30),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
            onPressed: () => Navigator.pushNamed(context, "/tenantPayment"),
            child: const Text("Login", style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }

  Widget _buildLandlordAuth() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(20.0),
      child: Column(
        children: [
          Image.asset("assets/logo.png", height: 80),
          const SizedBox(height: 20),
          _buildTextField("Email", landlordEmailController),
          const SizedBox(height: 20),
          _buildTextField("Password", landlordPasswordController, obscure: true),
          TextButton(
            onPressed: () => Navigator.pushNamed(context, "/landlordReset"),
            child: const Text("Forgot Password?", style: TextStyle(color: Colors.white)),
          ),
          const SizedBox(height: 30),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
            onPressed: () => Navigator.pushNamed(context, "/dashboard"),
            child: const Text("Login", style: TextStyle(color: Colors.white)),
          ),
          const SizedBox(height: 15),

          _buildTextField("Full Name", fullNameController),
          const SizedBox(height: 15),
          _buildTextField("Email", signupEmailController),
          const SizedBox(height: 15),
          _buildTextField("Phone Number", phoneController),
          const SizedBox(height: 15),
          _buildTextField("Password", signupPasswordController, obscure: true),
          const SizedBox(height: 20),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.purple),
            onPressed: () {
              Navigator.pushNamed(context, "/propertySetup");
            },
            child: const Text("Sign Up", style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }

  Widget _buildTextField(String label, TextEditingController controller, {bool obscure = false}) {
    return TextField(
      controller: controller,
      obscureText: obscure,
      style: const TextStyle(color: Colors.white),
      decoration: InputDecoration(
        labelText: label,
        labelStyle: const TextStyle(color: Colors.white),
        border: const OutlineInputBorder(borderSide: BorderSide(color: Colors.green)),
      ),
    );
  }
}