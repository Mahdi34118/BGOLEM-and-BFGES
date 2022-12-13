package edu.cmu.tetrad.search;
import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class PriorST {
    static List<List<Double>> records = new ArrayList<>();
        public static double score_ST(int chld , int...prnt ) {
            double scorep = 0;
            for (int i = 0; i < prnt.length; i++) {

                scorep += records.get(chld).get(prnt[i]);
            }
            return scorep;

        }
        public PriorST()
        {
//            address for linux FileReader("/home/home/Documents/Mehdi/PyCausal_All/method/DTI")
//            address for windows F:\mahdi\ARSHAD\project\Tetrad\previousversionsTetCmd\handchange
//            address for server : /home/abagheri/PyCausal_All/" +
//            "py_causal_development_V1.4_THirdPrior_WithgetStructure/method/DTI

//            /home/mlcm-cpu/Documents/Mehdi/mahdi/PyCausal_All/method/DTI/

//            /home/home/Desktop/Mehdi/PyCausal_All" +
//            "/py_causal_development_V1.4_THirdPrior_WithgetStructure/method/DTI/
            try (BufferedReader br = new BufferedReader(new FileReader("/home/mlcm-cpu/Documents/Mehdi/mahdi/PyCausal_All/method/DTI_175/foo.csv"))) {
                    
                String line;
                while ((line = br.readLine()) != null) {
                    String[] values = line.split(",");

                    Double[] values2 = new Double[values.length];
                    for (int i = 0; i < values.length ; i++) {
                        values2[i] = Double.parseDouble(values[i]);
                    }

                    records.add(Arrays.asList(values2));

                }
            }
            catch (Exception e){
                System.out.print(e.toString());
            }
//            System.out.print(score_ST(0 , new int[]{1 , 2 , 15}));
        }

    }

