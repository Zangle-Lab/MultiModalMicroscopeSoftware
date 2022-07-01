function [ ph ] = DPC_tik( IDPC, H, reg )
%DPC_TIK recover phase ph based on DPC data Idpc, with transfer function H
%and regularization parameter reg
%ph = sum_i (H_i^* F(Idpc_i))/(sum_i(abs(H_i)^2)+reg
%
% This code is distributed under a creative commons attributable
% sharealike license. This license allows you to remix, adapt, and build 
% upon this work, as long as the authors are credited and the modified code
% is redistributed under the same license.
%
% reference: 
% Lei Tian and Laura Waller, "Quantitative differential phase contrast
% imaging in an LED array microscope," Opt. Express 23, 11394-11403 (2015)

F = @(x) fftshift(fft2(ifftshift(x)));
Ft = @(x) fftshift(ifft2(ifftshift(x)));

if size(IDPC,3)==size(H,3)
    ph = -real(Ft(sum(F(IDPC).*conj(H),3)./(sum(abs(H).^2,3)+reg)));
else
    error('DPC data should have the same dimension as the transfer function');
end
end

