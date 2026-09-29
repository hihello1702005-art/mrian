import 'dart:convert'; import 'package:http/http.dart' as http;
class ApiClient {ApiClient(this.baseUrl,{http.Client? client}):_client=client??http.Client();final String baseUrl;final http.Client _client;String? token;
 Future<dynamic> get(String path) async {final response=await _client.get(Uri.parse('$baseUrl/api$path'),headers:_headers());if(response.statusCode>=400)throw ApiException(response.statusCode,response.body);return jsonDecode(response.body);}
 Future<dynamic> post(String path,Map<String,dynamic> body) async {final response=await _client.post(Uri.parse('$baseUrl/api$path'),headers:_headers(),body:jsonEncode(body));if(response.statusCode>=400)throw ApiException(response.statusCode,response.body);return response.body.isEmpty?null:jsonDecode(response.body);}
 Map<String,String> _headers()=>{'Content-Type':'application/json',if(token!=null)'Authorization':'Bearer $token'};
 Future<Map<String,dynamic>> liveKitToken(String showId) async => Map<String,dynamic>.from(await post('/livekit/token',{'show_id':showId}) as Map);
}class ApiException implements Exception {ApiException(this.status,this.body);final int status;final String body;@override String toString()=> 'API $status: $body';}
