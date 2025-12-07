#!/bin/bash

set -e

CHROOT=/mnt

echo "[*] Detecting root filesystem…"

# Detect LVM root first
LVM_ROOT=$(lsblk -rpo NAME,TYPE,MOUNTPOINT | grep "lvm" | grep -v "swap" | awk '{print $1}' | head -n1)

# Detect non-LVM root
ROOT_PART=$(lsblk -rpo NAME,MOUNTPOINT | grep -v "/mnt" | grep -v "/run/live" | grep -E "ext4|xfs|btrfs|ext3|ext2" | awk '$2==""{print $1}' | head -n1)

if [[ -n "$LVM_ROOT" ]]; then
    ROOT="$LVM_ROOT"
    echo "[+] LVM root detected: $ROOT"
else
    ROOT="$ROOT_PART"
    echo "[+] Standard root detected: $ROOT"
fi

if [[ -z "$ROOT" ]]; then
    echo "[!] ERROR: No root filesystem detected."
    exit 1
fi

# Activate LVM
echo "[*] Activating LVM volume groups…"
vgchange -ay || true

echo "[*] Mounting root filesystem at $CHROOT…"
mkdir -p "$CHROOT"
mount "$ROOT" "$CHROOT"

echo "[*] Detecting boot partition…"
BOOT_PART=$(lsblk -rpo NAME,TYPE | grep part | grep -E "boot|efi" | awk '{print $1}' | head -n1)

if [[ -z "$BOOT_PART" ]]; then
    echo "[!] No dedicated /boot or EFI partition found. Assuming /boot is inside root."
else
    echo "[+] Boot partition detected: $BOOT_PART"
    mkdir -p "$CHROOT/boot"
    mount "$BOOT_PART" "$CHROOT/boot" || true
fi

echo "[*] Detecting EFI partition…"
EFI_PART=$(lsblk -rpo NAME,FSTYPE | grep vfat | awk '{print $1}' | head -n1)

if [[ -n "$EFI_PART" ]]; then
    echo "[+] EFI partition detected: $EFI_PART"
    mkdir -p "$CHROOT/boot/efi"
    mount "$EFI_PART" "$CHROOT/boot/efi" || true
else
    echo "[!] No EFI partition detected."
fi

echo "[*] Binding virtual filesystems…"
mount --bind /dev "$CHROOT/dev"
mount --bind /dev/pts "$CHROOT/dev/pts"
mount --bind /proc "$CHROOT/proc"
mount --bind /sys "$CHROOT/sys"
mount --bind /run "$CHROOT/run"

echo "[*] Copying DNS resolver config…"
cp /etc/resolv.conf "$CHROOT/etc/" || true

echo ""
echo "============================================================"
echo "  ENTERING CHROOT ENVIRONMENT"
echo "  Type 'exit' or press Ctrl+D to leave the chroot."
echo "============================================================"
echo ""

chroot "$CHROOT" /bin/bash || true

echo ""
echo "[*] Cleaning up and unmounting…"

umount -lf "$CHROOT/dev/pts" || true
umount -lf "$CHROOT/dev" || true
umount -lf "$CHROOT/proc" || true
umount -lf "$CHROOT/sys" || true
umount -lf "$CHROOT/run" || true

if mountpoint -q "$CHROOT/boot/efi"; then
    umount -lf "$CHROOT/boot/efi" || true
fi

if mountpoint -q "$CHROOT/boot"; then
    umount -lf "$CHROOT/boot" || true
fi

umount -lf "$CHROOT" || true

echo "[+] Chroot session finished. All unmounted safely."
