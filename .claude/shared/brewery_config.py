#!/usr/bin/env python3
"""
Shared configuration for Brygd brewery documentation system

This module contains constants and configuration values that are shared
across multiple skills and tools.
"""

# Valid owner roles for documentation
VALID_OWNERS = [
    "VD",
    "Bryggmästaren",
    "Bryggmästare",
    "Bryggerichef",
    "Kvalitetsansvarig",
    "Lageransvarig",
    "Marknadsansvarig",
    "Ekonomiansvarig",
    "Inköpsansvarig",
    "Miljöansvarig",
    "Logistikansvarig",
    "Fastighetsansvarig",
    "Skyddsombud",
    "Säljare",
    "Besöksansvarig"
]

# Valid status values
VALID_STATUSES = ["published", "draft", "archived"]
