Cloud PRNG seed
###############

`Pollinate
<https://github.com/dustinkirkland/pollinate>`_ is
a client application that retrieves entropy from one or more Pollen servers and
seeds the local Pseudo Random Number Generator (PRNG).

Pollinate is essential for systems in cloud environments, ensuring secure and
adequate PRNG seeding. Starting with Ubuntu 14.04 LTS (Trusty Tahr), Ubuntu
cloud images include the Pollinate client, which seeds the PRNG with input from
`Ubuntu's entropy service <https://entropy.ubuntu.com>`_ during the first boot.

Regression tests: `pollen_test.go
<https://bazaar.launchpad.net/~kirkland/pollen/trunk/view/head:/pollen_test.go>`_.
