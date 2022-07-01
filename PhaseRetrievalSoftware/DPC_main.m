% last edited by Lei Tian (lei_tian@alum.mit.edu), 04/29/2015
% last edited by Edward R. Polanco, Tarek E. Moustafa, Thomas A. Zangle,
% 05/24/22
%
% reference: 
% Lei Tian and Laura Waller, "Quantitative differential phase contrast
% imaging in an LED array microscope," Opt. Express 23, 11394-11403 (2015)
%
% This code is distributed under a creative commons attributable
% sharealike license. This license allows you to remix, adapt, and build 
% upon this work, as long as the authors are credited and the modified code
% is redistributed under the same license.
%
% reference: 
% Lei Tian and Laura Waller, "Quantitative differential phase contrast
% imaging in an LED array microscope," Opt. Express 23, 11394-11403 (2015)

clear all; clc; close all;

% add source code here
addpath('...\DPC');

% % Define Fourier operators
F = @(x) fftshift(fft2(ifftshift(x)));
Ft = @(x) fftshift(ifft2(ifftshift(x)));
% froot should point to the folder containing data
froot = '.\data\';
% fstart is what you want to name the file
% default form is: 'Experiment_date_pos#_frame#.mat
fstart = 'Experiment_date_';
numPos =3;
numFrame = 1;

tic
for jj = 1:numPos
    pos = jj;
%     tic
    for ii = 1:numFrame
        frame = ii;
        % where you put the data
        filedir = ([froot,'pos',num2str(pos),'\','frame',num2str(frame),'\']);

        % setup output folder here
        out_dir = (froot);
%         Next line is commented because output directory should already
%         exist
%         mkdir(out_dir);

        % find all the figures
        imglist = dir([filedir,'Image_*.tiff']);
        %% images from directory    
        nfiles = length(imglist);    % Number of files found
        for ii=1:nfiles
           currentfilename = [filedir,imglist(ii).name];
           currentimage=double(imread(currentfilename));
           Ih{ii} = currentimage;
        end
%         gets tiff for top image
        D = dir(currentfilename);
        timestamp = D.datenum;

        % load system parameters
        SystemSetupDPC();
        
        % illumination angles are at right angles to each other
        rot_an = [90 180]; 

        nAngle = length(rot_an);

        %% calculating DPC Transfer function
        Hi = zeros(Np(1),Np(2),nAngle);

        % what's the illumination NA used?
        NA_illum = NA;
        source_led = 1;
        for dd = 1:2
            % source shape?
            S = Dsource_LR(rot_an(dd), NA_illum, lambda, u, v);
            S = S.*source_led;
            % calculate transfer function
            [Hr, Hi(:,:,dd)] = DPCTransFunc(pupil, S);
        end


           % calculate DPC image
        IDPC = zeros(Np(1),Np(2),nAngle);   
        for dd = 1:nAngle
            if dd==1
                I1 = Ih{((dd-1)*4)+3};
                I2 = Ih{((dd-1)*4)+2};
            end
            if dd>1
                I1 = Ih{((dd-2)*4)+1};
                I2 = Ih{((dd-2)*4)+4};
            end
            IDPC(:,:,dd) = (I1-I2)./(I1+I2);
        end
        intensity = I1;

        % NEED TO TUNE THE FOLLOWING REGULARIZATION PARAMETERS BASED ON
        % EXPERIMENTAL SNR
        reg2 = 1e-3; % regularization parameter
        
        % calculate phase by deconvolution
        ph_dpc =  DPC_tik(IDPC, Hi, reg2);
        Dsub=-ph_dpc(:,:);
        % uncomment next few lines to view phase images as they come out
%         figure;
%         imagesc(-Dsub)
%         colormap('gray')
%         axis off
%         colorbar
        Phase = -Dsub;
        PhC = IDPC;
        BF = I1+I2;
        save([out_dir, fstart,'pos',num2str(pos),'_frame',num2str(frame)], ...
        'Phase', 'BF', 'timestamp')


    end
%     toc
end
toc