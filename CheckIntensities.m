###############################################################################
# CheckIntensities.m
# Author: Eddie Polanco, Tarek E. Moustafa, Thomas A. Zangle
#
# This code is distributed under a creative commons attributable
# sharealike license. This license allows you to remix, adapt, and build 
# upon this work, as long as the authors are credited and the modified code
# is redistributed under the same license.
###############################################################################

path = 'C:\Users\DPC2\Documents\Eddie\EddiesDPCCode_121121\LEDCenteringData\pos2\';
numIter = 100;
bot = zeros(numIter,1);
top = zeros(numIter,1);
left = zeros(numIter,1);
right = zeros(numIter,1);



for ii = 1:numIter
%     bot(ii) = mean(mean(imread([path,'bot_',num2str(ii-1),'.jpg'])));
%     top(ii) = mean(mean(imread([path,'top_',num2str(ii-1),'.jpg'])));
%     left(ii) = mean(mean(imread([path,'left_',num2str(ii-1),'.jpg'])));
%     right(ii) = mean(mean(imread([path,'right_',num2str(ii-1),'.jpg'])));
    bot(ii) = mean(mean(imread([path, 'frame', num2str(ii),'\', 'Image_',num2str(ii),'B.tiff'])));
    top(ii) = mean(mean(imread([path, 'frame', num2str(ii),'\', 'Image_',num2str(ii),'T.tiff'])));
    left(ii) = mean(mean(imread([path, 'frame', num2str(ii),'\', 'Image_',num2str(ii),'L.tiff'])));
    right(ii) = mean(mean(imread([path, 'frame', num2str(ii),'\', 'Image_',num2str(ii),'R.tiff'])));
end
intensities = [bot,top,left,right];
figure
boxplot(intensities)


