program TestAll;
var
  x, y, i, q, r: integer;
  b, c: boolean;
begin
  writeln();                 { pusta linia }
  writeln(1, 2, 67);         { writeln z wieloma argumentami (integer) }

  readln(x);                 { wejście: integer }
  y := -1;                   { unarny minus }

  if x < 0 then
  begin
    y := 10;
  end
  else
  begin
    y := x * 2;
  end;

  while y < 10 do
    y := y + 1;

  q := y div 3;
  r := y mod 3;
  writeln(q, r);

  { boolean / logika }
  b := true;
  c := false;
  if not c and (b or (x <> 0)) then
    writeln(x, y)
  else
  begin
    begin end;              { pusty blok }
    writeln(0);
  end;

  repeat
    y := y + 2;
  until (y >= 20) and b;

  for i := 1 to 3 do
    writeln(i, y);

  for i := 3 downto 1 do
  begin
    x := x + i;
    writeln(x);
  end;

  { porównania w if: '=' mapuje się na '==' w C }
  if (x = y) or (x <= y) or (x >= y) then
    writeln(111)
  else
    writeln(222);

  writeln(x, y);
end.
