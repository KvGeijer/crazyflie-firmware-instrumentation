%% MOdelling PID hovering shifts

file_name = 'logPIDHoverNoSkip.csv';
file_path = ['decoded/',file_name];

time_shifts = load(file_path);

acfpacfnorm(time_shifts)

AR_inds = [18,19];
MA_inds = [20];

model_init = initModelARMA(AR_inds, MA_inds);
model =  pem(iddata(time_shifts'), model_init); 

filtered_shifts = resid(iddata(time_shifts'),model).y;

acfpacfnorm(filtered_shifts);

%% Remove outliers and model

clean_shifts = [];

m_shifts = mean(time_shifts);

for shift = time_shifts
    if abs(shift - m_shifts) < 0.02
        clean_shifts = [clean_shifts; shift];
    end
end

acfpacfnorm(clean_shifts)

%% Functions

function acfpacfnorm(data, maxOrd)
%Gives some analysis of the data, plotting ACF, PACF, Normplot

N = length(data);

if (nargin < 2)
    %Changed here so that it won't be too hard to see
    maxOrd = min(100,round(N/4));
end

figure
subplot(311)
acf(data, maxOrd, 0.05, 1, 0 ,0);
title("ACF")
subplot(312)
pacf(data, maxOrd, 0.05, 1, 0);
title("PACF")
subplot(313)
normplot(data);
%plotNTdist(data)
title("Normplot")


end

function model = initModelARMA(A_coefs,C_coefs)
% Creates the idpoly you want as an empty initial model, given what terms
% you want in your ARMA.
%
% INPUTS:    
%           A_coefs: Which places do we want terms in A polynomial
%           C_coefs: Which places do we want terms in C polynomial
%
% Output: The initial model created with idpoly. It does not contain any
% guesses, just initializes variables to zero.

A_poly = [1, zeros(1,max(A_coefs))];
A_free = zeros(1,max(A_coefs)+1);   
if (isempty(A_coefs))
    A_poly = [];
end

for i = A_coefs
    A_free(i+1) = 1; 
end


C_poly = [1, zeros(1,max(C_coefs))];
C_free = zeros(1, 1 + max(C_coefs));
if (isempty(C_coefs))
    C_poly = [];
end

for i = C_coefs
    C_free(i+1) = 1; 
end

A_free = logical(A_free);
C_free = logical(C_free);


model = idpoly(A_poly,[],C_poly);
if (~isempty(A_coefs)); model.Structure.a.Free = A_free; end

end

function isWhite(e)
% Is your resulting noise white?

maxOrd = min(60,round(length(e)/4));

figure
subplot(411)
acf(e, maxOrd, 0.05, 1, 0, 0);
title("ACF of e")
subplot(412)
pacf(e, maxOrd, 0.05, 1, 0);
title("PACF of e")
subplot(413)
%normplot(data);
plotNTdist(e)
title("Is it gaussian distributed?")
subplot(414)
whitenessTest(e);

end
