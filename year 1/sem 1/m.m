% Define the integration parameters
a = 4;
b = 6;
n = 10;
dx = (b - a) / n;

% Define the inline function
f = @(x) 6 * log(x.^3 + 5);

% 1. Trapezoidal Rule
x_trap = a:dx:b;
y_trap = f(x_trap);
trap = (dx / 2) * (y_trap(1) + 2 * sum(y_trap(2:end-1)) + y_trap(end));
trap = round(trap, 6);

% 2. Midpoint Rule
x_mid = (a + dx/2):dx:(b - dx/2);
mid = dx * sum(f(x_mid));
mid = round(mid, 6);

% 3. Simpson's Rule
% Create alternating weights [1, 4, 2, 4, ..., 4, 1]
w = ones(1, n + 1);
w(2:2:end-1) = 4;
w(3:2:end-2) = 2;
simp = (dx / 3) * sum(w .* y_trap);
simp = round(simp, 6);

% Display the results
fprintf('Trapezoidal Rule: %.6f\n', trap);
fprintf('Midpoint Rule: %.6f\n', mid);
fprintf('Simpson''s Rule: %.6f\n', simp);