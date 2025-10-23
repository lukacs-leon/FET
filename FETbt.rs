fn main() {
   let points = 2004; //place back 'mut'
   const TARGET : i32 = 1000;
   let difference = points - TARGET;
   if points >= TARGET {
    println!("The user can wish for something. (Difference: {})", difference);
   } else {
    println!("The user can't wish anything. (Difference: {})", difference * -1);
   }
}