% The code here is setting up P; enter your answer further down.
% (We encourage you to take the time to look through the code
% and ask for help if you do not understand it. While it is not
% necessary to understand what is going on in the code below to
% answer the question, you will need to use loops in later courses.)
P = zeros(25);
for i=1:25
    for j=i+1:min(i+6,25)
        P(i,j) = 1/6;
    end
end
for i = 1:6
    P(25-6+i, 25) = min((i+1)/6, 1);
end

% Evaluate the product:
P_two_turns = P * P
% (Note that it is not P that you need to extract the row from,
% because you are asked to provide the row of probilities starting
% from square 1 after TWO turns, not after just one turn.)

% Extract the appropriate row
Ans = P_two_turns(1, :)

