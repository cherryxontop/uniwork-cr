% Enter the SL vector below
SL = [2 16; 3 15; 4 14; 22 5; 23 6; 24 7]


% We have included some Matlab code below. You do not need to understand it all to answer the question, but
% we encourage you to look at the loops and ask for help if you do not see how they work. It is very common
% to use loops in this sort of project.

% The number of squares
n = 25; 

% Construct the P matrix first by ignoring the snakes and ladders

% The probability of taking a step from i to j is determined by the die
P = zeros(n);
for i=1:n
    for j=i+1:min(i+6,n)
        P(i,j) = 1/6;
    end
end

% Consider the case when the step could be greater than the number
% of places remaining on the board
for i = 1:6
    P(n-6+i, n) = min((i+1)/6, 1);
end

% Adjust the probability when landing on the start of a ladder
% or tail of a snake
no_SL = height(SL);
for i= 1:no_SL
    for j=1:n
        if j == SL(i,2)
            P(SL(i,1),j) = 1;
        else
            P(SL(i,1),j) = 0;
        end
    end
end

% Construct the s vector
s = ones([n-1 1]);

% Extract tildeP
tildeP = P(1:(n-1),1:(n-1));

% Solve for h below
I_mat = eye(n-1);
h = (I_mat - tildeP) \ s

% Plot the expect game duration
plot_SL_game(SL, h)

