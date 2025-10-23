fn main() {
    println!("{}", can_wish());
}
fn can_wish() -> String {
   let points = 2004; //place back 'mut'
   const TARGET : i32 = 1000;
   let difference = points - TARGET;
   let message = if points >= TARGET {
       format!("The user can wish for something. (Difference: {})", difference)
   } else {
       format!("The user can't wish anything. (still missing: {})", -difference)
   };
   message
}