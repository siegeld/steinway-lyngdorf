# Steinway P100 CLI Quick Reference

## Basic Usage
```bash
./run_cli.sh <command> [options]
```

## Power Commands
```bash
./run_cli.sh on              # Turn on main zone
./run_cli.sh off             # Turn off main zone
./run_cli.sh toggle          # Toggle main zone power
./run_cli.sh status          # Show power status for all zones

./run_cli.sh zone2 on        # Turn on Zone 2
./run_cli.sh zone2 off       # Turn off Zone 2
```

## Volume Commands
```bash
./run_cli.sh volume get                      # Show current volume levels
./run_cli.sh volume set -- -40               # Set to -40 dB (use -- for negative)
./run_cli.sh volume up                       # Increase by 0.5 dB
./run_cli.sh volume down                     # Decrease by 0.5 dB
./run_cli.sh volume up --step 2              # Increase by 2 dB
./run_cli.sh volume mute                     # Mute main zone
./run_cli.sh volume unmute                   # Unmute main zone

# Zone 2 volume
./run_cli.sh volume set -- -50 --zone2      # Set Zone 2 to -50 dB
./run_cli.sh volume up --zone2              # Increase Zone 2 volume
./run_cli.sh volume mute --zone2            # Mute Zone 2
```

## Monitor Mode
```bash
./run_cli.sh monitor                         # Monitor forever
./run_cli.sh monitor --duration 60          # Monitor for 60 seconds
./run_cli.sh monitor --feedback 0           # Minimal output
./run_cli.sh monitor --feedback 1           # Status updates (default)
./run_cli.sh monitor --feedback 2           # All commands + echoes
```

## Global Options
```bash
--host <ip>     # Override device IP/hostname
--port <port>   # Override TCP port (default: 84)
--debug         # Enable debug logging
--help          # Show help
```

## Examples
```bash
# Use different host
./run_cli.sh --host 192.168.1.100 status

# Debug connection issues
./run_cli.sh --debug status

# Monitor with specific host
./run_cli.sh --host p100.local monitor

# Quick power cycle
./run_cli.sh off && sleep 5 && ./run_cli.sh on
```

## Environment Variables
Create `.env` file with:
```
STEINWAY_HOST=p100asp1
STEINWAY_PORT=84
STEINWAY_LOG_LEVEL=INFO
```

## Tips
- No need to activate venv when using `run_cli.sh`
- Monitor mode shows TX (→) in green, RX (←) in blue
- Press Ctrl+C to stop monitoring
- Use `--debug` to troubleshoot connection issues