clc
clear all
close all

%% Defining parameters from Model_3.html

age = linspace(1,100);
asc_dist = 	-9.80;
beta_dist_young = 0.531;
beta_dist_adult = 0.00172;
beta_dist_old = -0.0302;
beta_dist = zeros(1,100);

%% Computing beta_dist as a function of age 

for i=1:100
    if i <= 18
        beta_dist(i) = asc_dist + beta_dist_young * i;
    elseif i <= 65
        beta_dist(i) = beta_dist(18) + beta_dist_adult * (i-18);
    elseif i <= 100
        beta_dist(i) = beta_dist(65) + beta_dist_old * (i-65);
    end
end

%% Plotting beta_dist
% Only people older than 8 years old are taken into account, as this is the
% age where they begin moving alone

plot(age(8:100),beta_dist(8:100))
hold on 
title("\beta_{dist} with regard to the age")
xlabel("Age [years]")
ylabel("\beta_{dist}")