import 'package:flutter_test/flutter_test.dart'; import 'package:meradion/main.dart';
void main(){testWidgets('shows MeradioN splash branding',(tester)async{await tester.pumpWidget(const MeradionApp());expect(find.text("Meradio'N"),findsOneWidget);expect(find.text('Your Sound. Your Stories.'),findsOneWidget);});}
