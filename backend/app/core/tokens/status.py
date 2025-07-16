"""
Defines token lifecycle states for one-time-use JWTs in the Project Nox authentication system.

These statuses represent the various states a token can occupy from issuance through expiration or redemption.
Used in validation logic, database records, and audit/debug tooling.
"""

from enum import Enum


class TokenStatus(str, Enum):
    """
    Represents the lifecycle status of a single-use token.

    Values:
        PENDING: Token was generated but not yet issued or sent.
        ISSUED: Token has been issued and is eligible for redemption.
        REDEEMED: Token has been successfully used.
        EXPIRED: Token expired before it could be redeemed.
        INVALID: Token was manually voided due to security or logic reasons.
        CANCELLED: Token was invalidated due to user-initiated cancellation.
        FAILED: Token failed to be delivered or encountered an issue.
        REPLACED: Token has been superseded by a newer token.
    """

    PENDING = "pending"
    ISSUED = "issued"
    REDEEMED = "redeemed"
    EXPIRED = "expired"
    INVALID = "invalid"
    CANCELLED = "cancelled"
    FAILED = "failed"
    REPLACED = "replaced"
    # Add more above this comment, as needed.
