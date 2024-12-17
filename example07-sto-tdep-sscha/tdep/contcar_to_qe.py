#!/usr/bin/python
# Final function including the writing process
def process_files_write_final(input_prefix, output_prefix):
    # Ask user for the value of N
    try:
        N = int(input("Enter the number of files to process (N): "))
        if N < 1:
            raise ValueError("N must be a positive integer.")
        elif N >= 1000:
            raise ValueError("N must be less than 1000.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    for X in range(1, N+1):
        input_file = f"{input_prefix}{X:04d}"
        output_file = f"{output_prefix}{X:04d}"
        try:
            # Read the contcar file
            with open(input_file, 'r') as f:
                lines = f.readlines()
            print(f'Now writing file number {X}:')
    
            # Parse the lines according to the rules
            if len(lines) < 8:
                raise ValueError("File does not have the required number of lines.")
    
            # Step 1: Parse the scaling factor
            scaling_factor = float(lines[1].strip())
            if abs(scaling_factor - 1) > 1e-5:
                raise ValueError("Scaling factor is not 1")
    
            # Step 2: Parse the cell vectors
            v1 = list(lines[2].strip().split())
            v2 = list(lines[3].strip().split())
            v3 = list(lines[4].strip().split())
            # Step 3: Parse atomic species
            atomic_species = lines[5].strip().split()
    
            # Step 4: Parse number of atoms
            num_atoms = list(map(int, lines[6].strip().split()))
            if len(num_atoms) != len(atomic_species):
                raise ValueError("Number of atomic species does not match number of atom counts.")
            tot_sum = sum(num_atoms)
            # Step 5: Determine coordinate type
            coord_line = lines[7].strip()
            if coord_line[0].lower() == 'd':
                direct_flag = True
            elif coord_line[0].lower() == 'c':
                direct_flag = False
            else:
                raise ValueError("Coordinates should be either direct or cartesian")
    
            # Step 6: Parse atom positions and validate
            il, i, cur_sum = 0, 0, 0
            atom_positions_list = []
            for line in lines[8:]:
                line = line.strip()
                if il < tot_sum:
                    il += 1
                    parts = line.split(maxsplit=7)
                    if len(parts) < 8:
                        raise ValueError(f"Atom position line format incorrect at line {il}.")
    
                    try:
                        # Extract components
                        x, y, z = map(float, parts[:3])
                        latt_vec_prec = len(parts[0]) 
                        long_string = " ".join(parts[3:]).strip()
                        long_parts = long_string.replace(":", " : ").split()
    
                        # Validate and extract long_string components
                        if len(long_parts) != 6 or long_parts[0] != "site" or long_parts[2] != "species" or long_parts[4] != ":":
                            raise ValueError(f"Malformed atom information: {long_string}")
                        site = int(long_parts[1])
                        species_id = int(long_parts[3])
                        atom_type = long_parts[5]
    
                    except (ValueError, IndexError):
                        raise ValueError(f"Error parsing atom position line {il}: {line}")
    
                    if site != il:
                        raise ValueError("Missing or repeating sites.")
                    if site <= num_atoms[i] + cur_sum and species_id == i + 1 and atom_type == atomic_species[i]:

                        formatted = f"{atomic_species[i]}    " + "   ".join(parts[:3])
                        atom_positions_list.append(formatted)
                        if site == num_atoms[i] + cur_sum:
                            cur_sum += num_atoms[i]
                            i += 1
                else:
                    # Skip lines beyond the expected number of sites
                    if line.strip():
                        continue
    
            # Write the qe_conf file
            with open(output_file, 'w') as f:
                f.write(f" # cell\n")
                f.write(f"&SYSTEM\n")
                f.write(f"   ibrav = 0\n")
                f.write(f"   celldm(1) = 1.889726125458\n")
                f.write(f"   nat = {tot_sum}\n")
                f.write(f"   ntyp = {len(atomic_species)}\n")
                f.write("/\n")
                f.write("CELL_PARAMETERS {alat}\n")
                f.write(f"     "+"   ".join(v1)+"\n")
                f.write(f"     "+"   ".join(v2)+"\n")
                f.write(f"     "+"   ".join(v3)+"\n")
    
                f.write("ATOMIC_SPECIES\n")
                for iele in atomic_species:
                    f.write(f"   {iele}     {iele}_MASS    {iele}_PSEUDO\n")
                if direct_flag:
                    f.write("ATOMIC_POSITIONS {crystal}\n")
                else:
                    f.write("ATOMIC_POSITIONS {angstrom}\n")
                for atom_position in atom_positions_list:
                    f.write(atom_position + "\n")
            print(f'File {X} writing complete.')    
        except Exception as e:
            print(f'Error processing {input_file}: {e}')

# Run the process for the provided files and write the output
qe_path = "qe_conf"
contcar_path = "contcar_conf"
print(f'Converting files from {contcar_path} to {qe_path}:')
process_files_write_final(contcar_path, qe_path)

