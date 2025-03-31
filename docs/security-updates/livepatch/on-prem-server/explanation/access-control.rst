Access control
##############

Access to a Livepatch on-prem instance is gated such that clients are
authenticated before they can download patches. Access control is
managed by means of generated tokens. These tokens act as a way of both
authenticating client machines and assigning a tier to each machine,
i.e. determining how and when patches get rolled out.

See this
`how-to <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/how-to/use_livepatch_client>`__
to understand how to generate tokens.
