# Built by John W. Harms ##
# Version 0.01 -- Initial Build ##
# Version 0.02 -- Refactored to be added as module to different project ##
# Last Change 9 June 15

import math
import random
import numpy
import numpy.linalg


def Covariance(covAssetPosX, covAssetPosY, covAssetPosZ, covConjPosX, covConjPosY, covConjPosZ,
               covAssetMat00, covAssetMat01, covAssetMat02, covAssetMat10, covAssetMat11, covAssetMat12,
               covAssetMat20, covAssetMat21, covAssetMat22,  covConjMat00, covConjMat01, covConjMat02,
               covConjMat10, covConjMat11, covConjMat12, covConjMat20, covConjMat21, covConjMat22,
               covSamples, covCombRadi):

    # Created by David RC Dayton (http://www.github.com/David-RC-Dayton)
    default_sigma = 1.0
    default_samples = 10000

    def collision_prob(ap, sp, ac, sc,
                       sigma=default_sigma, hbr=20.0,
                       n_sim=default_samples):
        # normalize input arguments
        ap = [float(x) for x in ap]
        sp = [float(x) for x in sp]
        ac = [[float(x) for x in y] for y in ac]
        sc = [[float(x) for x in y] for y in sc]
        sigma = float(sigma)
        hbr = float(hbr)
        n_sim = int(n_sim)

        random.seed(0)  # set seed for consistent results
        rand_vec = lambda: [random.gauss(0, 1) for _ in range(3)]
        # scale covariance to match sigma & find Cholesky decomposition
        asset_sig = [[x * sigma for x in y] for y in ac]
        satellite_sig = [[x * sigma for x in y] for y in sc]
        asset_chol = numpy.linalg.cholesky(asset_sig)
        satellite_chol = numpy.linalg.cholesky(satellite_sig)
        # shift sampled points from spacecraft position & store calculated distance
        euclid_dist = lambda a, b: \
            math.sqrt(sum([(x - y) ** 2 for x, y in zip(a, b)]))
        hit = 0
        for _ in range(n_sim):
            asset_gauss = rand_vec()
            satellite_gauss = rand_vec()
            asset_shift = numpy.dot(asset_chol, asset_gauss).tolist()
            satellite_shift = numpy.dot(satellite_chol, satellite_gauss).tolist()
            asset_point = [x + y for x, y in zip(asset_shift, ap)]
            satellite_point = [x + y for x, y in zip(satellite_shift, sp)]
            if euclid_dist(asset_point, satellite_point) <= hbr:
                hit += 1
        # find probability of collision
        return float(hit) / n_sim

    asset_pos = [covAssetPosX, covAssetPosY, covAssetPosZ]
    satellite_pos = [covConjPosX, covConjPosY, covConjPosZ]
    asset_cov = [[covAssetMat00, covAssetMat01, covAssetMat02],
                 [covAssetMat10, covAssetMat11, covAssetMat12],
                 [covAssetMat20, covAssetMat21, covAssetMat22]]
    satellite_cov = [[covConjMat00, covConjMat01, covConjMat02],
                     [covConjMat10, covConjMat11, covConjMat12],
                     [covConjMat20, covConjMat21, covConjMat22]]

    covRss = math.sqrt((math.pow((covAssetPosX - covConjPosX), 2) + (math.pow((covAssetPosY - covConjPosY), 2)) + (
        math.pow((covAssetPosZ - covConjPosZ), 2))))
    covSigma1 = collision_prob(asset_pos, satellite_pos, asset_cov, satellite_cov, 1, covCombRadi, covSamples)
    covSigma2 = collision_prob(asset_pos, satellite_pos, asset_cov, satellite_cov, 2, covCombRadi, covSamples)
    covSigma3 = collision_prob(asset_pos, satellite_pos, asset_cov, satellite_cov, 3, covCombRadi, covSamples)
    if covSigma1 > 0:
        covSigma1_prob = "(1 in %d chance)" % collision_prob(asset_pos, satellite_pos, asset_cov, satellite_cov,
                                                             1, covCombRadi, covSamples) ** -1
    else:
        covSigma1_prob = "There is a 0% probability of collision at 1 sigma"
    if covSigma2 > 0:
        covSigma2_prob = "(1 in %d chance)" % collision_prob(asset_pos, satellite_pos, asset_cov, satellite_cov,
                                                             2, covCombRadi, covSamples) ** -1
    else:
        covSigma2_prob = "There is a 0% probability of collision at 2 sigma"
    if covSigma3 > 0:
        covSigma3_prob = "(1 in %d chance)" % collision_prob(asset_pos, satellite_pos, asset_cov, satellite_cov,
                                                             3, covCombRadi, covSamples) ** -1
    else:
        covSigma3_prob = "There is a 0% probability of collision at 3 sigma"
    covSigma_out = "Distance between the center of the two error elipsoids is: %09.7f meters " \
                   "\n1 Sigma Probibility: %s %s \n2 Sigma Probibility: %s %s \n3 Sigma Probibility: %s %s"\
                   % (covRss, covSigma1, covSigma1_prob, covSigma2, covSigma2_prob, covSigma3, covSigma3_prob)
    return covSigma_out
