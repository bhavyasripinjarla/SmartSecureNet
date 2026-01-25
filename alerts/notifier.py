def notify_user(ssid, assessment):
    """
    Notifies the user about a high-risk Wi-Fi network
    """
    print("\n🚨 SECURITY ALERT 🚨")
    print(f"⚠️  High-risk Wi-Fi detected: {ssid}")
    print(f"Risk Level: {assessment['risk_level']}")

    if assessment.get("reasons"):
        print("Reasons:")
        for reason in assessment["reasons"]:
            print(f" - {reason}")

    print("Recommended Action: VPN enabled or disconnect Wi-Fi\n")
