# FET - Family Energy Token
## Structure
- backend: rust
  - data operating
    - counting points
    - syncronise the data through blockchain
  - makes the point purchase
- UI: swift/flutter
  - shows the indicators
## Business modell
### Cashflow
1. User1 (parent) purchase points for crypto or usd.
2. User1 give points for user2 (child) (it couldn't undo just burn with minus). If user1 give some minus to user2 the points are burned.
3. If user2 reaches the limit, the points burned and user2 gets a star.
