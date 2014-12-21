@interface Fraction: NSObject

@property int numerator, denominator;

-(void) print;
//-(void) setNumerator: (int) n;
//-(void) setDenominator: (int) d;

//-(int) numerator;
//-(int) denominator;
-(double) convertToNum;

-(void) setTo: (int) n over: (int) d;


@end
