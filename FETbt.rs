use std::io::{self, Write};

fn main() {
    let mut points = read_integer("Enter starting points (integer): ");
    println!("{}", can_wish(points));
    loop {
      let change_points = read_integer("Eneter points to change (integer): ");
      if 0 == change_points {
         break;
      } else {
         points = change_points + points
      }
      println!("{}", can_wish(points));
    }
    println!("{}", can_wish(points));
}

fn read_integer(prompt: &str) -> i32 {
    loop {
        print!("{}", prompt);
        io::stdout().flush().unwrap();
        let mut line = String::new();
        if io::stdin().read_line(&mut line).is_err() {
            eprintln!("Input error, please try again.");
            continue;
        }
        match line.trim().parse::<i32>() {
            Ok(n) => return n,
            Err(_) => {
                eprintln!("Invalid integer, please try again.");
                continue;
            }
        }
    }
}

fn can_wish(points: i32) -> String {
   const TARGET: i32 = 1000;
   let difference = points - TARGET;
   if points >= TARGET {
       format!("User can wish for something. (Difference: {})", difference)
   } else {
       format!("User can't wish anything. (Still missing: {})", -difference)
   }
}